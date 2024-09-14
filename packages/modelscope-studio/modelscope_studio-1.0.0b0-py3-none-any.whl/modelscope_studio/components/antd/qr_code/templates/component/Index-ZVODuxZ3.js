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
      const c = l[1], r = c.split("_"), _ = (...f) => {
        const b = f.map((u) => f && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
          type: u.type,
          detail: u.detail,
          timestamp: u.timeStamp,
          clientX: u.clientX,
          clientY: u.clientY,
          targetId: u.target.id,
          targetClassName: u.target.className,
          altKey: u.altKey,
          ctrlKey: u.ctrlKey,
          shiftKey: u.shiftKey,
          metaKey: u.metaKey
        } : u);
        return t.dispatch(c.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (r.length > 1) {
        let f = {
          ...s.props[r[0]] || {}
        };
        o[r[0]] = f;
        for (let u = 1; u < r.length - 1; u++) {
          const h = {
            ...s.props[r[u]] || {}
          };
          f[r[u]] = h, f = h;
        }
        const b = r[r.length - 1];
        return f[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _, o;
      }
      const d = r[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function K() {
}
function Q(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function V(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return K;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(e) {
  let t;
  return V(e, (i) => t = i)(), t;
}
const w = [];
function y(e, t = K) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (Q(e, c) && (e = c, i)) {
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
  function n(c) {
    o(c(e));
  }
  function l(c, r = K) {
    const _ = [c, r];
    return s.add(_), s.size === 1 && (i = t(o, n) || K), c(e), () => {
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
  getContext: q,
  setContext: P
} = window.__gradio__svelte__internal, Z = "$$ms-gr-antd-slots-key";
function B() {
  const e = y({});
  return P(Z, e);
}
const G = "$$ms-gr-antd-context-key";
function H(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = T(), i = W({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((r) => {
    i.slotKey.set(r);
  }), J();
  const s = q(G), o = ((c = g(s)) == null ? void 0 : c.as_item) || e.as_item, n = s ? o ? g(s)[o] : g(s) : {}, l = y({
    ...e,
    ...n
  });
  return s ? (s.subscribe((r) => {
    const {
      as_item: _
    } = g(l);
    _ && (r = r[_]), l.update((d) => ({
      ...d,
      ...r
    }));
  }), [l, (r) => {
    const _ = r.as_item ? g(s)[r.as_item] : g(s);
    return l.set({
      ...r,
      ..._
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const A = "$$ms-gr-antd-slot-key";
function J() {
  P(A, y(void 0));
}
function T() {
  return q(A);
}
const R = "$$ms-gr-antd-component-slot-context-key";
function W({
  slot: e,
  index: t,
  subIndex: i
}) {
  return P(R, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(i)
  });
}
function ye() {
  return q(R);
}
function $(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var U = {
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
        var c = arguments[l];
        c && (n = o(n, s(c)));
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
      for (var c in n)
        t.call(n, c) && n[c] && (l = o(l, c));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(U);
var ee = U.exports;
const I = /* @__PURE__ */ $(ee), {
  SvelteComponent: te,
  assign: ne,
  check_outros: se,
  component_subscribe: x,
  create_component: ie,
  destroy_component: oe,
  detach: X,
  empty: Y,
  flush: p,
  get_spread_object: E,
  get_spread_update: le,
  group_outros: re,
  handle_promise: ce,
  init: ue,
  insert: D,
  mount_component: ae,
  noop: m,
  safe_not_equal: _e,
  transition_in: v,
  transition_out: S,
  update_await_block_branch: fe
} = window.__gradio__svelte__internal;
function O(e) {
  let t, i, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: be,
    then: de,
    catch: me,
    value: 17,
    blocks: [, , ,]
  };
  return ce(
    /*AwaitedQRCode*/
    e[2],
    s
  ), {
    c() {
      t = Y(), s.block.c();
    },
    m(o, n) {
      D(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, i = !0;
    },
    p(o, n) {
      e = o, fe(s, e, n);
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
      o && X(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function me(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function de(e) {
  let t, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: I(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-qr-code"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].props,
    z(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    },
    {
      value: (
        /*$mergedProps*/
        e[0].props.value ?? /*$mergedProps*/
        e[0].value
      )
    }
  ];
  let o = {};
  for (let n = 0; n < s.length; n += 1)
    o = ne(o, s[n]);
  return t = new /*QRCode*/
  e[17]({
    props: o
  }), {
    c() {
      ie(t.$$.fragment);
    },
    m(n, l) {
      ae(t, n, l), i = !0;
    },
    p(n, l) {
      const c = l & /*$mergedProps, $slots*/
      3 ? le(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: I(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-qr-code"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && E(
        /*$mergedProps*/
        n[0].props
      ), l & /*$mergedProps*/
      1 && E(z(
        /*$mergedProps*/
        n[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, l & /*$mergedProps*/
      1 && {
        value: (
          /*$mergedProps*/
          n[0].props.value ?? /*$mergedProps*/
          n[0].value
        )
      }]) : {};
      t.$set(c);
    },
    i(n) {
      i || (v(t.$$.fragment, n), i = !0);
    },
    o(n) {
      S(t.$$.fragment, n), i = !1;
    },
    d(n) {
      oe(t, n);
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
function pe(e) {
  let t, i, s = (
    /*$mergedProps*/
    e[0].visible && O(e)
  );
  return {
    c() {
      s && s.c(), t = Y();
    },
    m(o, n) {
      s && s.m(o, n), D(o, t, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      1 && v(s, 1)) : (s = O(o), s.c(), v(s, 1), s.m(t.parentNode, t)) : s && (re(), S(s, 1, 1, () => {
        s = null;
      }), se());
    },
    i(o) {
      i || (v(s), i = !0);
    },
    o(o) {
      S(s), i = !1;
    },
    d(o) {
      o && X(t), s && s.d(o);
    }
  };
}
function he(e, t, i) {
  let s, o, n;
  const l = M(() => import("./qr-code-UkrkaKE-.js"));
  let {
    gradio: c
  } = t, {
    props: r = {}
  } = t;
  const _ = y(r);
  x(e, _, (a) => i(15, s = a));
  let {
    _internal: d = {}
  } = t, {
    value: f
  } = t, {
    as_item: b
  } = t, {
    visible: u = !0
  } = t, {
    elem_id: h = ""
  } = t, {
    elem_classes: k = []
  } = t, {
    elem_style: C = {}
  } = t;
  const [j, F] = H({
    gradio: c,
    props: s,
    _internal: d,
    value: f,
    visible: u,
    elem_id: h,
    elem_classes: k,
    elem_style: C,
    as_item: b
  });
  x(e, j, (a) => i(0, o = a));
  const N = B();
  return x(e, N, (a) => i(1, n = a)), e.$$set = (a) => {
    "gradio" in a && i(6, c = a.gradio), "props" in a && i(7, r = a.props), "_internal" in a && i(8, d = a._internal), "value" in a && i(9, f = a.value), "as_item" in a && i(10, b = a.as_item), "visible" in a && i(11, u = a.visible), "elem_id" in a && i(12, h = a.elem_id), "elem_classes" in a && i(13, k = a.elem_classes), "elem_style" in a && i(14, C = a.elem_style);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && _.update((a) => ({
      ...a,
      ...r
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, value, visible, elem_id, elem_classes, elem_style, as_item*/
    65344 && F({
      gradio: c,
      props: s,
      _internal: d,
      value: f,
      visible: u,
      elem_id: h,
      elem_classes: k,
      elem_style: C,
      as_item: b
    });
  }, [o, n, l, _, j, N, c, r, d, f, b, u, h, k, C, s];
}
class ge extends te {
  constructor(t) {
    super(), ue(this, t, he, pe, _e, {
      gradio: 6,
      props: 7,
      _internal: 8,
      value: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), p();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), p();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), p();
  }
  get value() {
    return this.$$.ctx[9];
  }
  set value(t) {
    this.$$set({
      value: t
    }), p();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), p();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), p();
  }
}
export {
  ge as I,
  ye as g,
  y as w
};
