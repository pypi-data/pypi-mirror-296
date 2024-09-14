async function Y() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function D(t) {
  return await Y(), t().then((e) => e.default);
}
function z(t) {
  const {
    gradio: e,
    _internal: o,
    ...s
  } = t;
  return Object.keys(o).reduce((i, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], r = c.split("_"), f = (..._) => {
        const b = _.map((u) => _ && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
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
        return e.dispatch(c.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (r.length > 1) {
        let _ = {
          ...s.props[r[0]] || {}
        };
        i[r[0]] = _;
        for (let u = 1; u < r.length - 1; u++) {
          const h = {
            ...s.props[r[u]] || {}
          };
          _[r[u]] = h, _ = h;
        }
        const b = r[r.length - 1];
        return _[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, i;
      }
      const d = r[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function K() {
}
function L(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function M(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return K;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function g(t) {
  let e;
  return M(t, (o) => e = o)(), e;
}
const k = [];
function y(t, e = K) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function i(c) {
    if (L(t, c) && (t = c, o)) {
      const r = !k.length;
      for (const f of s)
        f[1](), k.push(f, t);
      if (r) {
        for (let f = 0; f < k.length; f += 2)
          k[f][0](k[f + 1]);
        k.length = 0;
      }
    }
  }
  function n(c) {
    i(c(t));
  }
  function l(c, r = K) {
    const f = [c, r];
    return s.add(f), s.size === 1 && (o = e(i, n) || K), c(t), () => {
      s.delete(f), s.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: n,
    subscribe: l
  };
}
const {
  getContext: v,
  setContext: P
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function V() {
  const t = y({});
  return P(T, t);
}
const Z = "$$ms-gr-antd-context-key";
function G(t) {
  var c;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = J(), o = Q({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((r) => {
    o.slotKey.set(r);
  }), H();
  const s = v(Z), i = ((c = g(s)) == null ? void 0 : c.as_item) || t.as_item, n = s ? i ? g(s)[i] : g(s) : {}, l = y({
    ...t,
    ...n
  });
  return s ? (s.subscribe((r) => {
    const {
      as_item: f
    } = g(l);
    f && (r = r[f]), l.update((d) => ({
      ...d,
      ...r
    }));
  }), [l, (r) => {
    const f = r.as_item ? g(s)[r.as_item] : g(s);
    return l.set({
      ...r,
      ...f
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const q = "$$ms-gr-antd-slot-key";
function H() {
  P(q, y(void 0));
}
function J() {
  return v(q);
}
const A = "$$ms-gr-antd-component-slot-context-key";
function Q({
  slot: t,
  index: e,
  subIndex: o
}) {
  return P(A, {
    slotKey: y(t),
    slotIndex: y(e),
    subSlotIndex: y(o)
  });
}
function ht() {
  return v(A);
}
function W(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var B = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function o() {
      for (var n = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (n = i(n, s(c)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return o.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var c in n)
        e.call(n, c) && n[c] && (l = i(l, c));
      return l;
    }
    function i(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(B);
var $ = B.exports;
const I = /* @__PURE__ */ W($), {
  SvelteComponent: tt,
  assign: et,
  check_outros: nt,
  component_subscribe: x,
  create_component: st,
  destroy_component: ot,
  detach: F,
  empty: R,
  flush: p,
  get_spread_object: E,
  get_spread_update: it,
  group_outros: lt,
  handle_promise: rt,
  init: ct,
  insert: U,
  mount_component: ut,
  noop: m,
  safe_not_equal: at,
  transition_in: w,
  transition_out: S,
  update_await_block_branch: ft
} = window.__gradio__svelte__internal;
function O(t) {
  let e, o, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: dt,
    then: mt,
    catch: _t,
    value: 16,
    blocks: [, , ,]
  };
  return rt(
    /*AwaitedFloatButtonBackTop*/
    t[2],
    s
  ), {
    c() {
      e = R(), s.block.c();
    },
    m(i, n) {
      U(i, e, n), s.block.m(i, s.anchor = n), s.mount = () => e.parentNode, s.anchor = e, o = !0;
    },
    p(i, n) {
      t = i, ft(s, t, n);
    },
    i(i) {
      o || (w(s.block), o = !0);
    },
    o(i) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        S(l);
      }
      o = !1;
    },
    d(i) {
      i && F(e), s.block.d(i), s.token = null, s = null;
    }
  };
}
function _t(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function mt(t) {
  let e, o;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: I(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-float-button-back-top"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    /*$mergedProps*/
    t[0].props,
    z(
      /*$mergedProps*/
      t[0]
    ),
    {
      slots: (
        /*$slots*/
        t[1]
      )
    }
  ];
  let i = {};
  for (let n = 0; n < s.length; n += 1)
    i = et(i, s[n]);
  return e = new /*FloatButtonBackTop*/
  t[16]({
    props: i
  }), {
    c() {
      st(e.$$.fragment);
    },
    m(n, l) {
      ut(e, n, l), o = !0;
    },
    p(n, l) {
      const c = l & /*$mergedProps, $slots*/
      3 ? it(s, [l & /*$mergedProps*/
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
          "ms-gr-antd-float-button-back-top"
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
      }]) : {};
      e.$set(c);
    },
    i(n) {
      o || (w(e.$$.fragment, n), o = !0);
    },
    o(n) {
      S(e.$$.fragment, n), o = !1;
    },
    d(n) {
      ot(e, n);
    }
  };
}
function dt(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function bt(t) {
  let e, o, s = (
    /*$mergedProps*/
    t[0].visible && O(t)
  );
  return {
    c() {
      s && s.c(), e = R();
    },
    m(i, n) {
      s && s.m(i, n), U(i, e, n), o = !0;
    },
    p(i, [n]) {
      /*$mergedProps*/
      i[0].visible ? s ? (s.p(i, n), n & /*$mergedProps*/
      1 && w(s, 1)) : (s = O(i), s.c(), w(s, 1), s.m(e.parentNode, e)) : s && (lt(), S(s, 1, 1, () => {
        s = null;
      }), nt());
    },
    i(i) {
      o || (w(s), o = !0);
    },
    o(i) {
      S(s), o = !1;
    },
    d(i) {
      i && F(e), s && s.d(i);
    }
  };
}
function pt(t, e, o) {
  let s, i, n;
  const l = D(() => import("./float-button.back-top-BpyGSwSQ.js"));
  let {
    gradio: c
  } = e, {
    props: r = {}
  } = e;
  const f = y(r);
  x(t, f, (a) => o(14, s = a));
  let {
    _internal: d = {}
  } = e, {
    as_item: _
  } = e, {
    visible: b = !0
  } = e, {
    elem_id: u = ""
  } = e, {
    elem_classes: h = []
  } = e, {
    elem_style: C = {}
  } = e;
  const [j, X] = G({
    gradio: c,
    props: s,
    _internal: d,
    visible: b,
    elem_id: u,
    elem_classes: h,
    elem_style: C,
    as_item: _
  });
  x(t, j, (a) => o(0, i = a));
  const N = V();
  return x(t, N, (a) => o(1, n = a)), t.$$set = (a) => {
    "gradio" in a && o(6, c = a.gradio), "props" in a && o(7, r = a.props), "_internal" in a && o(8, d = a._internal), "as_item" in a && o(9, _ = a.as_item), "visible" in a && o(10, b = a.visible), "elem_id" in a && o(11, u = a.elem_id), "elem_classes" in a && o(12, h = a.elem_classes), "elem_style" in a && o(13, C = a.elem_style);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && f.update((a) => ({
      ...a,
      ...r
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    32576 && X({
      gradio: c,
      props: s,
      _internal: d,
      visible: b,
      elem_id: u,
      elem_classes: h,
      elem_style: C,
      as_item: _
    });
  }, [i, n, l, f, j, N, c, r, d, _, b, u, h, C, s];
}
class yt extends tt {
  constructor(e) {
    super(), ct(this, e, pt, bt, at, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), p();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), p();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), p();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), p();
  }
}
export {
  yt as I,
  ht as g,
  y as w
};
