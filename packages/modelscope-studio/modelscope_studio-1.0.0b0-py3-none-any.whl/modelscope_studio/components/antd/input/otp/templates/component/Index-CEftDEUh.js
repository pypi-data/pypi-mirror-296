async function L() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function M(e) {
  return await L(), e().then((t) => t.default);
}
function z(e) {
  const {
    gradio: t,
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], r = u.split("_"), _ = (...f) => {
        const p = f.map((a) => f && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return t.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: s
        });
      };
      if (r.length > 1) {
        let f = {
          ...s.props[r[0]] || {}
        };
        o[r[0]] = f;
        for (let a = 1; a < r.length - 1; a++) {
          const h = {
            ...s.props[r[a]] || {}
          };
          f[r[a]] = h, f = h;
        }
        const p = r[r.length - 1];
        return f[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _, o;
      }
      const d = r[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function K() {
}
function T(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Z(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return K;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(e) {
  let t;
  return Z(e, (i) => t = i)(), t;
}
const w = [];
function g(e, t = K) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(u) {
    if (T(e, u) && (e = u, i)) {
      const r = !w.length;
      for (const _ of s)
        _[1](), w.push(_, e);
      if (r) {
        for (let _ = 0; _ < w.length; _ += 2)
          w[_][0](w[_ + 1]);
        w.length = 0;
      }
    }
  }
  function n(u) {
    o(u(e));
  }
  function l(u, r = K) {
    const _ = [u, r];
    return s.add(_), s.size === 1 && (i = t(o, n) || K), u(e), () => {
      s.delete(_), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: l
  };
}
const {
  getContext: x,
  setContext: j
} = window.__gradio__svelte__internal, B = "$$ms-gr-antd-slots-key";
function G() {
  const e = g({});
  return j(B, e);
}
const H = "$$ms-gr-antd-context-key";
function J(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = W(), i = $({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((r) => {
    i.slotKey.set(r);
  }), Q();
  const s = x(H), o = ((u = y(s)) == null ? void 0 : u.as_item) || e.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = g({
    ...e,
    ...n
  });
  return s ? (s.subscribe((r) => {
    const {
      as_item: _
    } = y(l);
    _ && (r = r[_]), l.update((d) => ({
      ...d,
      ...r
    }));
  }), [l, (r) => {
    const _ = r.as_item ? y(s)[r.as_item] : y(s);
    return l.set({
      ...r,
      ..._
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const A = "$$ms-gr-antd-slot-key";
function Q() {
  j(A, g(void 0));
}
function W() {
  return x(A);
}
const V = "$$ms-gr-antd-component-slot-context-key";
function $({
  slot: e,
  index: t,
  subIndex: i
}) {
  return j(V, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(i)
  });
}
function ye() {
  return x(V);
}
function ee(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var R = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var n = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (n = o(n, s(u)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return i.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var u in n)
        t.call(n, u) && n[u] && (l = o(l, u));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(R);
var te = R.exports;
const O = /* @__PURE__ */ ee(te), {
  SvelteComponent: ne,
  assign: se,
  check_outros: ie,
  component_subscribe: P,
  create_component: oe,
  destroy_component: le,
  detach: U,
  empty: X,
  flush: b,
  get_spread_object: E,
  get_spread_update: re,
  group_outros: ce,
  handle_promise: ue,
  init: ae,
  insert: Y,
  mount_component: _e,
  noop: m,
  safe_not_equal: fe,
  transition_in: v,
  transition_out: S,
  update_await_block_branch: me
} = window.__gradio__svelte__internal;
function q(e) {
  let t, i, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: be,
    then: pe,
    catch: de,
    value: 18,
    blocks: [, , ,]
  };
  return ue(
    /*AwaitedInputOTP*/
    e[3],
    s
  ), {
    c() {
      t = X(), s.block.c();
    },
    m(o, n) {
      Y(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, i = !0;
    },
    p(o, n) {
      e = o, me(s, e, n);
    },
    i(o) {
      i || (v(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        S(l);
      }
      i = !1;
    },
    d(o) {
      o && U(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function de(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function pe(e) {
  let t, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: O(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-input-otp"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[1].elem_id
      )
    },
    /*$mergedProps*/
    e[1].props,
    z(
      /*$mergedProps*/
      e[1]
    ),
    {
      value: (
        /*$mergedProps*/
        e[1].props.value ?? /*$mergedProps*/
        e[1].value
      )
    },
    {
      slots: (
        /*$slots*/
        e[2]
      )
    },
    {
      onValueChange: (
        /*func*/
        e[16]
      )
    }
  ];
  let o = {};
  for (let n = 0; n < s.length; n += 1)
    o = se(o, s[n]);
  return t = new /*InputOTP*/
  e[18]({
    props: o
  }), {
    c() {
      oe(t.$$.fragment);
    },
    m(n, l) {
      _e(t, n, l), i = !0;
    },
    p(n, l) {
      const u = l & /*$mergedProps, $slots, value*/
      7 ? re(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: O(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-input-otp"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && E(
        /*$mergedProps*/
        n[1].props
      ), l & /*$mergedProps*/
      2 && E(z(
        /*$mergedProps*/
        n[1]
      )), l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          n[1].props.value ?? /*$mergedProps*/
          n[1].value
        )
      }, l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          n[2]
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          n[16]
        )
      }]) : {};
      t.$set(u);
    },
    i(n) {
      i || (v(t.$$.fragment, n), i = !0);
    },
    o(n) {
      S(t.$$.fragment, n), i = !1;
    },
    d(n) {
      le(t, n);
    }
  };
}
function be(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function he(e) {
  let t, i, s = (
    /*$mergedProps*/
    e[1].visible && q(e)
  );
  return {
    c() {
      s && s.c(), t = X();
    },
    m(o, n) {
      s && s.m(o, n), Y(o, t, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[1].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      2 && v(s, 1)) : (s = q(o), s.c(), v(s, 1), s.m(t.parentNode, t)) : s && (ce(), S(s, 1, 1, () => {
        s = null;
      }), ie());
    },
    i(o) {
      i || (v(s), i = !0);
    },
    o(o) {
      S(s), i = !1;
    },
    d(o) {
      o && U(t), s && s.d(o);
    }
  };
}
function ge(e, t, i) {
  let s, o, n;
  const l = M(() => import("./input.otp-8Q6hAtfi.js"));
  let {
    gradio: u
  } = t, {
    props: r = {}
  } = t;
  const _ = g(r);
  P(e, _, (c) => i(15, s = c));
  let {
    _internal: d = {}
  } = t, {
    value: f = ""
  } = t, {
    as_item: p
  } = t, {
    visible: a = !0
  } = t, {
    elem_id: h = ""
  } = t, {
    elem_classes: k = []
  } = t, {
    elem_style: C = {}
  } = t;
  const [I, D] = J({
    gradio: u,
    props: s,
    _internal: d,
    visible: a,
    elem_id: h,
    elem_classes: k,
    elem_style: C,
    as_item: p,
    value: f
  });
  P(e, I, (c) => i(1, o = c));
  const N = G();
  P(e, N, (c) => i(2, n = c));
  const F = (c) => {
    i(0, f = c);
  };
  return e.$$set = (c) => {
    "gradio" in c && i(7, u = c.gradio), "props" in c && i(8, r = c.props), "_internal" in c && i(9, d = c._internal), "value" in c && i(0, f = c.value), "as_item" in c && i(10, p = c.as_item), "visible" in c && i(11, a = c.visible), "elem_id" in c && i(12, h = c.elem_id), "elem_classes" in c && i(13, k = c.elem_classes), "elem_style" in c && i(14, C = c.elem_style);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && _.update((c) => ({
      ...c,
      ...r
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    65153 && D({
      gradio: u,
      props: s,
      _internal: d,
      visible: a,
      elem_id: h,
      elem_classes: k,
      elem_style: C,
      as_item: p,
      value: f
    });
  }, [f, o, n, l, _, I, N, u, r, d, p, a, h, k, C, s, F];
}
class we extends ne {
  constructor(t) {
    super(), ae(this, t, ge, he, fe, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 0,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), b();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), b();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  we as I,
  ye as g,
  g as w
};
